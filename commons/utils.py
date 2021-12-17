from django.core.paginator import Paginator


def get_pagination(request, itens, itens_per_page):
        paginated_itens = Paginator(itens, itens_per_page)

        if request.GET.get('pagina') is None:
            requested_page = 1
        else:
            requested_page = request.GET.get('pagina')
        
        selected_page = paginated_itens.get_page(requested_page)
        pages = range(1, paginated_itens.num_pages + 1)

        return selected_page, pages