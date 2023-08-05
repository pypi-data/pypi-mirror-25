from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.utils import six
from django.utils.translation import ugettext as _, ungettext

from misago.acl import add_acl
from misago.conf import settings
from misago.core.utils import clean_ids_list
from misago.threads.permissions import allow_merge_post, exclude_invisible_posts
from misago.threads.serializers import PostSerializer


MERGE_LIMIT = settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL


def posts_merge_endpoint(request, thread):
    if not thread.acl['can_merge_posts']:
        raise PermissionDenied(_("You can't merge posts in this thread."))

    try:
        posts = clean_posts_for_merge(request, thread)
    except PermissionDenied as e:
        return Response({'detail': six.text_type(e)}, status=400)

    first_post, merged_posts = posts[0], posts[1:]
    for post in merged_posts:
        post.merge(first_post)
        post.delete()

    if first_post.pk == thread.first_post_id:
        first_post.set_search_document(thread.title)
    else:
        first_post.set_search_document()

    first_post.save()

    first_post.update_search_vector()
    first_post.save(update_fields=['search_vector'])

    thread.synchronize()
    thread.save()

    thread.category.synchronize()
    thread.category.save()

    first_post.thread = thread
    first_post.category = thread.category

    add_acl(request.user, first_post)

    return Response(PostSerializer(first_post, context={'user': request.user}).data)


def clean_posts_for_merge(request, thread):
    posts_ids = clean_ids_list(
        request.data.get('posts', []),
        _("One or more post ids received were invalid."),
    )

    if len(posts_ids) < 2:
        raise PermissionDenied(_("You have to select at least two posts to merge."))
    elif len(posts_ids) > MERGE_LIMIT:
        message = ungettext(
            "No more than %(limit)s post can be merged at single time.",
            "No more than %(limit)s posts can be merged at single time.",
            MERGE_LIMIT,
        )
        raise PermissionDenied(message % {'limit': MERGE_LIMIT})

    posts_queryset = exclude_invisible_posts(request.user, thread.category, thread.post_set)
    posts_queryset = posts_queryset.filter(id__in=posts_ids).order_by('id')

    posts = []
    for post in posts_queryset:
        post.category = thread.category
        post.thread = thread

        allow_merge_post(request.user, post)

        if not posts:
            posts.append(post)
        else:
            authorship_error = _("Posts made by different users can't be merged.")
            if posts[0].poster_id:
                if post.poster_id != posts[0].poster_id:
                    raise PermissionDenied(authorship_error)
            else:
                if post.poster_id or post.poster_name != posts[0].poster_name:
                    raise PermissionDenied(authorship_error)

            if posts[0].pk != thread.first_post_id:
                if (posts[0].is_hidden != post.is_hidden or
                        posts[0].is_unapproved != post.is_unapproved):
                    raise PermissionDenied(_("Posts with different visibility can't be merged."))

            posts.append(post)

    if len(posts) != len(posts_ids):
        raise PermissionDenied(_("One or more posts to merge could not be found."))

    return posts
