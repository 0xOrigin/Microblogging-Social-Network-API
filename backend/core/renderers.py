from django.template import loader
from rest_framework import status
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer


# Override BrowsableAPIRenderer to add filter template support on altered list views
class BaseBrowsableAPIRenderer(BrowsableAPIRenderer):

    def get_filter_form(self, data, view, request):
        if not hasattr(view, 'get_queryset') or not hasattr(view, 'filter_backends'):
            return
        if 'pk' in view.kwargs:
            return

        queryset = view.get_queryset()
        elements = []
        for backend in view.filter_backends:
            if hasattr(backend, 'to_html'):
                html = backend().to_html(request, queryset, view)
                if html:
                    elements.append(html)

        if not elements:
            return

        template = loader.get_template(self.filter_template)
        context = {'elements': elements}
        return template.render(context)


class BaseJSONRenderer(JSONRenderer):

    def get_status_code(self, renderer_context):
        return int(renderer_context['response'].status_code)
    
    def get_success_response(self, data, status_code):
        success_response = {
            'status_code': status_code,
            'message': 'Success',
            'meta': None,
            'pagination': None,
            'data': list(),
        }
        if isinstance(data, dict): # If data is a dict, then it may contain pagination or any other metadata
            success_response['message'] = (
                data.pop('message', None) or
                data.pop('detail', None) or
                success_response['message']
            )
            success_response['meta'] = data.pop('meta', None)
            success_response['pagination'] = data.pop('pagination', None)
            success_response['data'] = data.pop('data', data)
        else: # If data is not a dict, then no pagination or any other metadata
            success_response['data'] = data

        if not success_response['meta']: # Remove meta key if it's None
            success_response.pop('meta')

        if not success_response['pagination']: # Remove pagination key if it's None
            success_response.pop('pagination')
        
        return success_response

    def get_error_response(self, data, status_code):
        error_response = {
            'status_code': status_code,
            'message': 'Fail',
            'error': data,
        }
        if isinstance(data, dict):
            error_response['message'] = (
                data.pop('message', None) or 
                data.pop('detail', None) or 
                error_response['message']
            )

        return error_response

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = self.get_status_code(renderer_context)

        if status_code == status.HTTP_204_NO_CONTENT: # Do not return any data for 204 responses (delete)
            return super(BaseJSONRenderer, self).render(data, accepted_media_type, renderer_context)

        if status_code >= status.HTTP_400_BAD_REQUEST:
            return super(BaseJSONRenderer, self).render(
                self.get_error_response(data, status_code), 
                accepted_media_type, 
                renderer_context
            )

        return super(BaseJSONRenderer, self).render(
            self.get_success_response(data, status_code), 
            accepted_media_type, 
            renderer_context
        )
