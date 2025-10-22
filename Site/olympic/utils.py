menu = [{'title': "Home Page", 'url_name': 'home'},
        {'title': "Olympiad Information", 'url_name': 'olympiads'},
        ]

additional_menu = [
    {'title': "Connect/Remove Notifications", 'url_name': 'notifications'},
]


class DataMixin:  # removing code duplication
    # paginate_by = 2  # ListView has built-in pagination, paginate_by = how many records to display on one page
    paginate_by = 6

    def get_user_context(self, **kwargs):  # creating the required context by default
        context = kwargs
        user_menu = menu.copy()
        if self.request.user.is_authenticated:
            user_menu += additional_menu.copy()
        context['menu'] = user_menu  # created context for menu
        return context
