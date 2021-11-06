from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.list import ListView
from django.forms.models import inlineformset_factory
from django.views.generic.base import TemplateResponseMixin, View
from .models import Task, TaskChekList
from .forms import TaskForm


# Список задач
class TaskListView(LoginRequiredMixin, ListView):
    template_name = 'task_tracker/task/list.html'
    model = Task
    context_object_name = 'tasks'


# Обновление и создания задачи
class TaskFormView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'task_tracker/task/form.html'
    task = None

    def get_task_checklist_formset(self, data=None):
        TaskFormSet = inlineformset_factory(
            Task,
            TaskChekList,
            fields=['title', 'is_completed'],
            extra=0, can_delete=True)
        return TaskFormSet(
            instance=self.task, data=data)

    def dispatch(self, *args, **kwargs):
        self.task = self.kwargs.get('pk', None)
        if self.task:
            self.task = get_object_or_404(Task, id=self.task)
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        task_form = TaskForm(instance=self.task)
        task_checklist_formset = self.get_task_checklist_formset()
        return self.render_to_response({
            'task_form': task_form,
            'task_checklist_formset': task_checklist_formset})

    def post(self, request, *args, **kwargs):
        task_form = TaskForm(data=request.POST, instance=self.task)
        task_checklist_formset = self.get_task_checklist_formset(
            data=request.POST)
        if task_form.is_valid() and task_checklist_formset.is_valid():
            task = task_form.save()
            task_checklists = task_checklist_formset.save(
                commit=False
            )
            for task_checklist in task_checklists:
                task_checklist.task = task
                task_checklist.save()
        task_deleted_objects = task_checklist_formset.deleted_objects
        for task_deleted in task_deleted_objects:
            task_deleted.delete()
        return redirect('task_tracker:task_list')
