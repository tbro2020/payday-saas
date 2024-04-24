from core.views import Change

class Employee(Change):
    template_name = "employee/change.html"

    def get(self, request, pk):
        self.kwargs['app'] = 'employee'
        self.kwargs['model'] = 'employee'
        return super().get(request, self.kwargs['app'], self.kwargs['model'], pk)
    
    def post(self, request, pk):
        self.kwargs['app'] = 'employee'
        self.kwargs['model'] = 'employee'
        return super().post(request, self.kwargs['app'], self.kwargs['model'], pk)