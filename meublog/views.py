from django.shortcuts import render, get_object_or_404

from meublog.models import Post


def listar_posts(request):
    posts = Post.publicados.all()
    return render(request, 'meublog/post/listarposts.html',
                  {'posts': posts})


def detalhar_post(request, ano, mes, dia, slug):
    post = get_object_or_404(Post, slug=slug, publicado__year= ano,
                             publicado__month= mes, publicado__day= dia)
    return render(request, 'meublog/post/detalharpost.html', {'post': post})
