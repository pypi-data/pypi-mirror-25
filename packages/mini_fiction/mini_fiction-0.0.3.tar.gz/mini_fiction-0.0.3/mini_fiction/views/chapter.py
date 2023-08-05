#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, abort, url_for, redirect, g, jsonify
from flask_login import current_user, login_required
from flask_babel import gettext
from pony.orm import db_session

from mini_fiction.forms.chapter import ChapterForm
from mini_fiction.models import Story, Chapter
from mini_fiction.utils.misc import diff2html
from .story import get_story

bp = Blueprint('chapter', __name__)


@bp.route('/story/<int:story_id>/chapter/all/', defaults={'chapter_order': None})
@bp.route('/story/<int:story_id>/chapter/<int:chapter_order>/')
@db_session
def view(story_id, chapter_order=None):
    story = get_story(story_id)
    user = current_user._get_current_object()

    allow_draft = user.is_staff or story.bl.is_contributor(user)

    if chapter_order is not None:
        chapter = Chapter.get(story=story_id, order=chapter_order)
        if not chapter:
            abort(404)
        if chapter.draft and not allow_draft:
            abort(404)
        page_title = chapter.autotitle[:80] + ' : ' + story.title
        prev_chapter = chapter.get_prev_chapter(allow_draft)
        next_chapter = chapter.get_next_chapter(allow_draft)
        if user.is_authenticated:
            chapter.bl.viewed(user)
        data = {
            'story': story,
            'chapter': chapter,
            'prev_chapter': prev_chapter,
            'next_chapter': next_chapter,
            'page_title': page_title,
            'allchapters': False,
            'robots_noindex': not story.published,
        }
    else:
        chapters = story.bl.select_accessible_chapters(user).order_by(Chapter.order, Chapter.id)[:]
        page_title = story.title + ' – все главы'
        if user.is_authenticated:
            for c in chapters:
                c.bl.viewed(user)
        data = {
            'story': story,
            'chapters': chapters,
            'page_title': page_title,
            'allchapters': True,
            'robots_noindex': not story.published,
        }

    return render_template('chapter_view.html', **data)


def _gen_preview(form, only_selected=False):
    title = request.form.get('title') or gettext('Chapter')
    sel_start = request.form.get('sel_start') or ''
    sel_end = request.form.get('sel_end') or ''
    notes_html = Chapter.bl.notes2html(request.form.get('notes', '')[:128000])

    if only_selected and sel_start.isdigit() and sel_end.isdigit():
        html = Chapter.bl.text2html(request.form.get('text', '')[:128000], start=int(sel_start), end=int(sel_end))
    else:
        html = Chapter.bl.text2html(request.form.get('text', '')[:128000])

    return {
        'preview_title': title,
        'preview_html': html,
        'notes_preview_html': notes_html,
    }


@bp.route('/story/<int:story_id>/chapter/add/', methods=('GET', 'POST'))
@db_session
@login_required
def add(story_id):
    story = Story.get(id=story_id)
    if not story:
        abort(404)
    user = current_user._get_current_object()
    if not story.bl.editable_by(user):
        abort(403)

    not_saved = False

    preview_data = {'preview_title': None, 'preview_html': None, 'notes_preview_html': None}

    form = ChapterForm()

    if request.form.get('act') in ('preview', 'preview_selected'):
        preview_data = _gen_preview(request.form, only_selected=request.form.get('act') == 'preview_selected')

        if request.form.get('ajax') == '1':
            return jsonify(
                success=True,
                html=render_template(
                    'includes/chapter_preview.html',
                    story=story,
                    chapter=None,
                    **preview_data
                )
            )

    elif form.validate_on_submit():
        chapter = Chapter.bl.create(
            story=story,
            editor=user,
            data={
                'title': form.title.data,
                'notes': form.notes.data,
                'text': form.text.data,
            },
        )
        if request.form.get('act') == 'publish':
            story.bl.publish_all_chapters(user)
        return redirect(url_for('chapter.edit', pk=chapter.id))
    elif request.method == 'POST':
        not_saved = True

    data = {
        'page_title': 'Добавление новой главы',
        'story': story,
        'chapter': None,
        'form': form,
        'saved': False,
        'not_saved': not_saved,
        'unpublished_chapters_count': Chapter.select(lambda x: x.story == story and x.draft).count(),
    }
    data.update(preview_data)

    return render_template('chapter_work.html', **data)


@bp.route('/chapter/<int:pk>/edit/', methods=('GET', 'POST'))
@db_session
@login_required
def edit(pk):
    chapter = Chapter.get(id=pk)
    if not chapter:
        abort(404)
    user = current_user._get_current_object()
    if not chapter.story.bl.editable_by(user):
        abort(403)

    chapter_data = {
        'title': chapter.title,
        'notes': chapter.notes,
        'text': chapter.text,
    }

    saved = False
    not_saved = False
    older_text = None
    chapter_text_diff = []

    preview_data = {'preview_title': None, 'preview_html': None, 'notes_preview_html': None}

    form = ChapterForm(data=chapter_data)

    if request.form.get('act') in ('preview', 'preview_selected'):
        preview_data = _gen_preview(request.form, only_selected=request.form.get('act') == 'preview_selected')

        if request.form.get('ajax') == '1':
            return jsonify(
                success=True,
                html=render_template(
                    'includes/chapter_preview.html',
                    story=chapter.story,
                    chapter=chapter,
                    **preview_data
                )
            )

    elif form.validate_on_submit():
        if request.form.get('older_md5'):
            older_text, chapter_text_diff = chapter.bl.get_diff_from_older_version(request.form['older_md5'])
        if not chapter_text_diff:
            chapter.bl.update(
                editor=user,
                data={
                    'title': form.title.data,
                    'notes': form.notes.data,
                    'text': form.text.data,
                }
            )
            saved = True
        else:
            form.text.errors.append(
                'Пока вы редактировали главу, её отредактировал кто-то другой. Ниже представлен '
                'список изменений, которые вы пропустили. Перенесите их в свой текст и сохраните '
                'главу ещё раз.'
            )
            not_saved = True
    elif request.method == 'POST':
        not_saved = True

    data = {
        'page_title': 'Редактирование главы «%s»' % chapter.autotitle,
        'story': chapter.story,
        'chapter': chapter,
        'form': form,
        'edit': True,
        'saved': saved,
        'not_saved': not_saved,
        'chapter_text_diff': chapter_text_diff,
        'diff_html': diff2html(older_text, chapter_text_diff) if chapter_text_diff else None,
        'unpublished_chapters_count': Chapter.select(lambda x: x.story == chapter.story and x.draft).count(),
    }
    data.update(preview_data)

    return render_template('chapter_work.html', **data)


@bp.route('/chapter/<int:pk>/delete/', methods=('GET', 'POST'))
@db_session
@login_required
def delete(pk):
    chapter = Chapter.get(id=pk)
    if not chapter:
        abort(404)
    user = current_user._get_current_object()
    if not chapter.story.bl.editable_by(user):
        abort(403)

    story = chapter.story

    if request.method == 'POST':
        chapter.bl.delete(editor=user)
        return redirect(url_for('story.edit', pk=story.id))

    page_title = 'Подтверждение удаления главы'
    data = {
        'page_title': page_title,
        'story': story,
        'chapter': chapter,
    }

    if g.is_ajax:
        html = render_template('includes/ajax/chapter_ajax_confirm_delete.html', page_title=page_title, story=story, chapter=chapter)
        return jsonify({'page_content': {'modal': html, 'title': page_title}})
    else:
        return render_template('chapter_confirm_delete.html', **data)


@bp.route('/chapter/<int:pk>/publish/', methods=('GET', 'POST',))
@db_session
@login_required
def publish(pk):
    chapter = Chapter.get(id=pk)
    if not chapter:
        abort(404)
    user = current_user._get_current_object()
    if not chapter.story.bl.editable_by(user):
        abort(403)

    chapter.bl.publish(user, chapter.draft)  # draft == not published
    if g.is_ajax:
        return jsonify({'success': True, 'story_id': chapter.story.id, 'chapter_id': chapter.id, 'published': not chapter.draft})
    else:
        return redirect(url_for('story.edit', pk=chapter.story.id))


@bp.route('/story/<int:story_id>/sort/', methods=('POST',))
@db_session
@login_required
def sort(story_id):
    story = Story.get(id=story_id)
    if not story:
        abort(404)
    if not story.bl.editable_by(current_user._get_current_object()):
        abort(403)

    if not request.json or not request.json.get('chapters'):
        return jsonify({'success': False, 'error': 'Invalid request'})

    try:
        new_order = [int(x) for x in request.json['chapters']]
    except:
        return jsonify({'success': False, 'error': 'Invalid request'})

    chapters = {c.id: c for c in story.chapters}
    if not new_order or set(chapters) != set(new_order):
        return jsonify({'success': False, 'error': 'Bad request: incorrect list'})
    else:
        for new_order_id, chapter_id in enumerate(new_order):
            chapters[chapter_id].order = new_order_id + 1
        return jsonify({'success': True})
