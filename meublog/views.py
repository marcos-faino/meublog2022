from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView

from meublog.forms import EmailForm, ComentarioModelForm
from meublog.models import Post, Comentario


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


class DetalharPostView(DetailView):
    template_name = "meublog/post/detalharpost.html"
    model = Post

    def _get_coments(self, id_post):
        try:
            return Comentario.objects.filter(post_id=id_post,
                                             ativo=True)
        except Comentario.DoesNotExist:
            raise Exception

    def get_context_data(self, **kwargs):
        context = super(DetalharPostView, self).get_context_data(**kwargs)
        context['coments'] = self._get_coments(self.object.id)
        return context


class ComentarioCreateView(CreateView):
    template_name = "meublog/post/comentarios.html"
    form_class = ComentarioModelForm

    def _get_post(self, id_post):
        try:
            post = Post.publicados.get(pk=id_post)
            return post
        except Post.DoesNotExist:
            raise Exception

    def get_context_data(self, **kwargs):
        context = super(ComentarioCreateView, self).get_context_data(**kwargs)
        context['post'] = self._get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form, **kwargs):
        post = self._get_post(self.kwargs['pk'])
        form.salvarComentario(post)
        return redirect('meublog:detalhe',
                        post.criado.year,
                        post.criado.month,
                        post.criado.day,
                        post.slug)
