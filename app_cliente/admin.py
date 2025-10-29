# app_cliente/admin.py

from django.contrib import admin
from .models import Cliente, Perro

# Inline para mostrar los perros relacionados directamente en la vista de Cliente
class PerroInline(admin.TabularInline): # O admin.StackedInline para una vista más expandida
    model = Perro
    extra = 0 # No muestra formularios vacíos por defecto
    fields = ('nombre', 'raza', 'fecha_nacimiento', 'temperamento', 'foto')
    readonly_fields = ('foto_thumbnail',) # Para mostrar la imagen en el admin
    classes = ['collapse'] # Colapsa la sección por defecto

    def foto_thumbnail(self, obj):
        if obj.foto:
            # Puedes ajustar el tamaño del thumbnail si lo necesitas
            return f'<img src="{obj.foto.url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'
        return "No hay foto"
    foto_thumbnail.short_description = 'Thumbnail'
    foto_thumbnail.allow_tags = True


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'email', 'telefono', 'direccion_corta', 'num_perros')
    search_fields = ('nombre', 'apellido', 'email', 'telefono', 'direccion')
    list_filter = ('apellido',) # Puedes añadir más campos para filtrar
    ordering = ('apellido', 'nombre') # Ordena por apellido y luego por nombre
    inlines = [PerroInline] # Incluye los perros del cliente en su vista de detalle

    # Campos que se muestran en la vista de detalle
    fieldsets = (
        (None, {
            'fields': ('nombre', 'apellido', 'email', 'telefono', 'direccion')
        }),
    )

    # Métodos personalizados para list_display
    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    nombre_completo.short_description = "Nombre Completo"
    nombre_completo.admin_order_field = 'apellido' # Permite ordenar por este campo

    def direccion_corta(self, obj):
        if obj.direccion:
            return obj.direccion[:50] + '...' if len(obj.direccion) > 50 else obj.direccion
        return "N/A"
    direccion_corta.short_description = "Dirección"

    def num_perros(self, obj):
        return obj.perros.count()
    num_perros.short_description = "Nº Perros"


@admin.register(Perro)
class PerroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'raza', 'cliente_link', 'fecha_nacimiento', 'foto_thumbnail')
    search_fields = ('nombre', 'raza', 'temperamento', 'cliente__nombre', 'cliente__apellido')
    list_filter = ('raza', 'cliente')
    ordering = ('nombre',)
    # Campos para la vista de detalle
    fieldsets = (
        (None, {
            'fields': ('nombre', 'raza', 'fecha_nacimiento', 'temperamento', 'cliente', 'foto')
        }),
    )
    readonly_fields = ('foto_preview',) # Para mostrar la imagen subida en la vista de edición

    def cliente_link(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        link = reverse("admin:app_cliente_cliente_change", args=[obj.cliente.id])
        return format_html('<a href="{}">{} {}</a>', link, obj.cliente.nombre, obj.cliente.apellido)
    cliente_link.short_description = "Dueño"
    cliente_link.admin_order_field = 'cliente__apellido' # Permite ordenar por el apellido del cliente

    def foto_thumbnail(self, obj):
        if obj.foto:
            return f'<img src="{obj.foto.url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'
        return "No hay foto"
    foto_thumbnail.short_description = 'Foto'
    foto_thumbnail.allow_tags = True

    def foto_preview(self, obj): # Mostrar una vista previa más grande en el formulario de edición
        if obj.foto:
            return f'<img src="{obj.foto.url}" width="150" height="150" style="object-fit: cover; border-radius: 8px;" />'
        return "No hay imagen subida"
    foto_preview.short_description = "Previsualización de Foto"
    foto_preview.allow_tags = True