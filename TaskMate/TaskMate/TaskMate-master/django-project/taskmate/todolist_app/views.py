from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TaskList
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
import json

# Web-based Task List (for rendering HTML)
@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manager = request.user
            instance.save()
        messages.success(request, "New Task Added!")
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(manager=request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        return render(request, 'todolist.html', {'all_tasks': all_tasks})

# Delete Task (Web-based)
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(TaskList, pk=task_id)
    if task.manager == request.user:
        task.delete()
        messages.success(request, "Task Deleted Successfully")
    else:
        messages.error(request, "Access Restricted, You Are Not Allowed")
    return redirect('todolist')

# Edit Task (Web-based)
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(TaskList, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task Edited Successfully")
        return redirect('todolist')
    return render(request, 'edit.html', {'task_obj': task})

# Mark Task as Completed (Web-based)
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(TaskList, pk=task_id)
    if task.manager == request.user:
        task.done = True
        task.save()
        messages.success(request, "Task Marked as Completed")
    else:
        messages.error(request, "Access Restricted, You Are Not Allowed")
    return redirect('todolist')

# Mark Task as Pending (Web-based)
@login_required
def pending_task(request, task_id):
    task = get_object_or_404(TaskList, pk=task_id)
    if task.manager == request.user:
        task.done = False
        task.save()
        messages.success(request, "Task Marked as Pending")
    else:
        messages.error(request, "Access Restricted, You Are Not Allowed")
    return redirect('todolist')

# API Endpoints
def api_get_tasks(request):
    tasks = TaskList.objects.all().values()
    return JsonResponse(list(tasks), safe=False)

def api_get_task(request, task_id):
    task = get_object_or_404(TaskList, pk=task_id)
    return JsonResponse({"id": task.id, "name": task.name, "done": task.done, "manager": task.manager.id})

@csrf_exempt
def api_create_task(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task = TaskList.objects.create(
            name=data.get("name"),
            done=data.get("done", False),
            manager=request.user  # Ensure authenticated user is set as manager
        )
        return JsonResponse({"id": task.id, "name": task.name, "done": task.done}, status=201)

@csrf_exempt
def api_update_task(request, task_id):
    task = get_object_or_404(TaskList, pk=task_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        task.name = data.get("name", task.name)
        task.done = data.get("done", task.done)
        task.save()
        return JsonResponse({"id": task.id, "name": task.name, "done": task.done})

@csrf_exempt
def api_delete_task(request, task_id):
    task = get_object_or_404(TaskList, pk=task_id)
    if request.method == "DELETE":
        task.delete()
        return JsonResponse({"message": "Task Deleted Successfully"}, status=200)

# Static Pages
def index(request):
    context = {'index_test': "Welcome index Page."}
    return render(request, 'index.html', context)

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        context = {"success": True}
        return render(request, "contact.html", context)
    return render(request, "contact.html")

def about(request):
    context = {
        "company_name": "TaskMate Management System",
        "mission": "Our mission is to provide excellent services to our customers.",
        "vision": "We aim to be a global leader in our industry by setting high standards.",
        "values": ["Integrity", "Innovation", "Customer Satisfaction", "Sustainability"]
    }
    return render(request, "about.html", context)
