from django.contrib import admin
from .models import NestUser, Note, Order, PrintPricing, PickupLocation, MyNotes
from django.utils.html import format_html

# Admin for NestUsers
@admin.register(NestUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_superuser', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_superuser', 'is_staff')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('subject', 'branch', 'semester', 'uploaded_by', 'is_approved', 'upload_date', 'view_note')
    list_filter = ('is_approved', 'branch', 'semester')
    search_fields = ('subject', 'description')
    actions = ['approve_notes']

    def view_note(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View Note</a>', obj.file.url)
        return "No document uploaded"

    view_note.short_description = "View Note"

    def approve_notes(self, request, queryset):
        queryset.update(is_approved=True)
    approve_notes.short_description = "Approve selected notes"

@admin.register(MyNotes)
class MyNotesAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'created_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'price', 'created_at')
    list_filter = ('status', 'pickup_location')
    search_fields = ('user__username', 'order_id')

@admin.register(PrintPricing)
class PrintPricingAdmin(admin.ModelAdmin):
    list_display = ('black_and_white_price', 'color_price', 'fast_print_surcharge', 'delivery_surcharge', 'tax_rate')

@admin.register(PickupLocation)
class PickupLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'open_time', 'close_time')
