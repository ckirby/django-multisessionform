# Create your views here.
from django.views.generic.base import View
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

class MultiSessionFormView(View):
    form_class = None
    template_name = None
    multisessionform = None
    
    def dispatch(self, request, *args, **kwargs):
        if not self.form_class:
            raise ImproperlyConfigured("No form_class defined")
        if not self.template_name:
            raise ImproperlyConfigured("No template_name defined")
        try:
            self.multisessionform = self.form_class.multisessionform_factory()
        except:
            raise ImproperlyConfigured("%s does not use the MultiSessionFormMixin" % self.form_class.__name__)

        try:
            self.pk = self.kwargs['pk']
        except:
            self.pk = None
                    
        try:
            self.form_field = self.kwargs['form_field']
        except:
            self.form_field = None
        
        return super(MultiSessionFormView, self).dispatch(request, *args, **kwargs)
        
    
    def get(self, request, *args, **kwargs):
        if self.pk:
            try:
                model_object = self.form_class.objects.get(pk = self.pk, user = request.user, form_status=self.form_class.FORM_INCOMPLETE) 
                if self.form_field:
                    form = self.multisessionform(self.form_field, instance = model_object)
                else:
                    return HttpResponseRedirect(model_object.get_absolute_url(), args=(self.pk, model_object.get_first_incomplete_field()))
            except:
                model_object = self.form_class()
                return HttpResponseRedirect(model_object.get_absolute_url()) 
        else:
            model_object = None
            form = self.multisessionform(self.form_field)
        try:
            complete = model_object.is_complete()
        except:
            complete = None
        return render_to_response(self.template_name, 
                                  {'form':form, "model":model_object, "complete":complete}, 
                                  context_instance = RequestContext(request)
                                 )
        
    def post(self, request, *args, **kwargs):
        if self.pk:
            try:
                model_object = self.form_class.objects.get(pk = self.pk, user = request.user, form_status=self.form_class.FORM_INCOMPLETE) 
                form = self.multisessionform(self.form_field, request.POST, instance = model_object)
                if form.is_valid():
                    msf_form = form.save()
                    return HttpResponseRedirect(model_object.get_absolute_url(),args = (self.pk, request.GET.get('next',self.form_field)))
            except:
                model_object = self.form_class()
                return HttpResponseRedirect(model_object.get_absolute_url()) 
        else:
            model_object = self.form_class()
            form = self.multisessionform(self.form_field, request.POST)
            if form.is_valid():
                msf_form = form.save(commit = False)
                msf_form.user = request.user
                msf_form.save()
                
                return HttpResponseRedirect(model_object.get_absolute_url(), args = (msf_form.pk,form.get_first_incomplete_field()))

        try:
            complete = model_object.is_complete()
        except:
            complete = None
        return render_to_response(self.template_name, 
                                  {'form':form, "model":model_object, "complete":complete}, 
                                  context_instance = RequestContext(request)
                                 )