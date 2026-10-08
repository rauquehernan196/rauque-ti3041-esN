from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    imagen = models.URLField(max_length=500, blank=True, null=True)
    archivado = models.BooleanField(default=False)

    @property
    def imagen_url(self):
        if self.imagen and self.imagen.strip().startswith('http'):
            return self.imagen.strip()

        imagenes = [
            'https://images.unsplash.com/photo-1581147036324-c17ac5e9dba0?auto=format&fit=crop&w=900&q=80',
            'https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=900&q=80',
            'https://images.unsplash.com/photo-1513467535980-fd81bc7f1186?auto=format&fit=crop&w=900&q=80',
            'https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=900&q=80',
            'https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=900&q=80',
            'https://images.unsplash.com/photo-1621905251918-48416bd8575a?auto=format&fit=crop&w=900&q=80',
            'https://images.unsplash.com/photo-1565043666747-69f6646db940?auto=format&fit=crop&w=900&q=80',
            'https://images.unsplash.com/photo-1592150621744-aca64f48394d?auto=format&fit=crop&w=900&q=80',
            'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=900&q=80',
            'https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=900&q=80',
        ]
        return imagenes[(self.pk or 1) % len(imagenes)]

    def __str__(self):
        return self.nombre