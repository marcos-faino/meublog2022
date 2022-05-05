from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from meublog.forms import EmailForm
from meublog.models import Post


class FormContatoView(FormView):
    template_name = 'meublog/post/enviarpost.html'
    form_class = EmailForm
    success_url = reverse_lazy('meublog:listar_posts')

    def get_post(self, id_post):
        try:
            return Post.publicados.get(pk=id_post)
        except Post.DoesNotExist:
            messages.error(self.request, 'Post não encontrado!')
            reverse_lazy('meublog:listar_posts')

    def get_context_data(self, **kwargs):
        context = super(FormContatoView, self).get_context_data(**kwargs)
        context['post'] = self.get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form):
        meupost = self.get_context_data()['post']
        form.enviar_email(meupost)
        messages.success(self.request, f'Post {meupost.titulo} '
                                       f'enviado com sucesso.')
        return super(FormContatoView, self).form_valid(form)

    def form_invalid(self, form):
        meupost = self.get_context_data()['post']
        messages.error(self.request, f'Post {meupost.titulo} '
                                       f'não enviado.')
        return super(FormContatoView, self).form_invalid(form)



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
