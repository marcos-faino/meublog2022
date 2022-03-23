from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from meublog.models import Post


class ListarPostsView(ListView):
    queryset = Post.publicados.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = "meublog/post/listarposts.html"


"""
def listar_posts(request):
    lista_objetos = Post.publicados.all()
    paginacao = Paginator(lista_objetos, 2) # dois posts por página
    page = request.GET.get('page')
    try:
        posts = paginacao.page(page)
    except PageNotAnInteger:
        posts = paginacao.page(1)
    except EmptyPage:
        posts = paginacao.page(paginacao.num_pages)
    return render(request, 'meublog/post/listarposts.html',
                  {'page': page, 'posts': posts})

"""


class DetalharPostView(DetailView):
    template_name = "meublog/post/detalharpost.html"
    model = Post


"""
def detalhar_post(request, ano, mes, dia, slug):
    post = get_object_or_404(Post, slug=slug, publicado__year=ano,
                             publicado__month=mes, publicado__day=dia)
    print(post)
    return render(request, 'meublog/post/detalharpost.html', {'post': post})
"""
