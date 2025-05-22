from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from .models import Resource, Comment
from django.contrib.auth.models import User
from .forms import ResourceForm, CommentForm

# List view (all users)
def resource_list(request):
    resources = Resource.objects.all().order_by('-created_at')
    categories = Resource.CATEGORY_CHOICES
    
    # Create a dictionary to organize resources by category
    grouped = {}
    for cat, cat_name in categories:
        grouped[cat] = []
    
    # Add each resource to the appropriate category list
    for res in resources:
        if res.category in grouped:
            grouped[res.category].append(res)
        else:
            # Handle any resources with categories not in CATEGORY_CHOICES
            if 'Other' in grouped:
                grouped['Other'].append(res)
    
    return render(request, 'resources/resource_list.html', {
        'grouped': grouped,
        'categories': categories,
    })

# Resource detail view (for modal and direct access)
@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    comments = resource.comments.all().order_by('-created_at')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # If AJAX request, return partial template for modal
        return render(request, 'resources/resource_detail_partial.html', {
            'resource': resource,
            'comments': comments
        })
    
    # If regular request, show full page
    return render(request, 'resources/resource_detail.html', {
        'resource': resource,
        'comments': comments
    })

# Add resource (admin only)
@user_passes_test(lambda u: u.is_staff)
def resource_add(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.created_by = request.user
            resource.save()
            messages.success(request, 'Resource added successfully!')
            return redirect('resources:resource_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResourceForm()
    
    if request.headers.get('HX-Request'):
        # If it's an HTMX request, return just the form
        return render(request, 'resources/resource_form.html', {'form': form, 'action': 'Add'})
    return render(request, 'resources/resource_list.html', {'form': form})

# Edit resource (admin only)
@user_passes_test(lambda u: u.is_staff)
def resource_edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource updated successfully!')
            return redirect('resources:resource_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resources/resource_form.html', {'form': form, 'action': 'Edit'})

# Delete resource (admin only)
@user_passes_test(lambda u: u.is_staff)
def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        messages.success(request, 'Resource deleted successfully!')
        return redirect('resources:resource_list')
    return render(request, 'resources/resource_confirm_delete.html', {'resource': resource})

# Add comment (authenticated users)
@login_required
def add_comment(request, resource_id):
    if request.method == 'POST':
        resource = get_object_or_404(Resource, id=resource_id)
        content = request.POST.get('content', '').strip()
        
        if content:
            comment = Comment.objects.create(
                resource=resource,
                user=request.user,
                content=content
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'user': comment.user.username,
                        'content': comment.content,
                        'created_at': comment.created_at.strftime('%b %d, %Y'),
                    }
                })
            
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty.')
            
    return redirect('resources:resource_list') 