from django.core.management.base import BaseCommand
from django.utils import timezone
from inventario.models import MarcaLlanta, Llanta, Inventario, Entradas
from taller.models import Taller
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Crear datos de ejemplo para inventario (Taller, MarcaLlanta, Llanta, Inventario, Entradas)'

    def handle(self, *args, **options):
        created = 0
        # Taller
        try:
            taller, _ = Taller.objects.get_or_create(
                id_empresa='TALLER001',
                defaults={'razon_social': 'Taller Ejemplo S.A.', 'direccion': 'Calle Falsa 123', 'telefono': '555-0101'}
            )
        except IntegrityError:
            taller = Taller.objects.filter(id_empresa='TALLER001').first()

        # Marcas
        marcas = ['Michelin', 'Pirelli', 'Continental']
        marca_objs = []
        for m in marcas:
            obj, created_flag = MarcaLlanta.objects.get_or_create(nombre=m)
            marca_objs.append(obj)
            if created_flag:
                created += 1

        # Llantas
        llantas_data = [
            {'marca': marca_objs[0], 'modelo': 'Primacy 4', 'ancho': '205', 'alto': '55', 'rin': '16', 'radial': 1},
            {'marca': marca_objs[1], 'modelo': 'Cinturato P7', 'ancho': '195', 'alto': '65', 'rin': '15', 'radial': 1},
            {'marca': marca_objs[2], 'modelo': 'SportContact', 'ancho': '225', 'alto': '45', 'rin': '17', 'radial': 1},
        ]
        llanta_objs = []
        for ld in llantas_data:
            obj, created_flag = Llanta.objects.get_or_create(
                marca=ld['marca'], modelo=ld['modelo'], ancho=ld['ancho'], alto=ld['alto'], rin=ld['rin'],
                defaults={'radial': ld.get('radial', 0)}
            )
            llanta_objs.append(obj)
            if created_flag:
                created += 1

        # Inventario
        inv_items = [
            {'id_inventario': 'INV001', 'empresa': taller, 'producto_clave': 'MIC-205-55-16', 'descripcion': 'Llanta Michelin Primacy 4 205/55 R16', 'marca': 'Michelin', 'ancho': 205, 'alto': 55, 'rin': 16, 'existencia': 10, 'precio': 120.50},
            {'id_inventario': 'INV002', 'empresa': taller, 'producto_clave': 'PIR-195-65-15', 'descripcion': 'Llanta Pirelli Cinturato 195/65 R15', 'marca': 'Pirelli', 'ancho': 195, 'alto': 65, 'rin': 15, 'existencia': 8, 'precio': 95.00},
            {'id_inventario': 'INV003', 'empresa': taller, 'producto_clave': 'CON-225-45-17', 'descripcion': 'Llanta Continental SportContact 225/45 R17', 'marca': 'Continental', 'ancho': 225, 'alto': 45, 'rin': 17, 'existencia': 5, 'precio': 150.75},
        ]
        inv_objs = []
        for it in inv_items:
            obj, created_flag = Inventario.objects.get_or_create(
                id_inventario=it['id_inventario'],
                defaults={
                    'empresa': it['empresa'], 'producto_clave': it['producto_clave'], 'descripcion': it['descripcion'],
                    'marca': it['marca'], 'ancho': it['ancho'], 'alto': it['alto'], 'rin': it['rin'], 'existencia': it['existencia'], 'precio': it['precio']
                }
            )
            inv_objs.append(obj)
            if created_flag:
                created += 1

        # Entradas (link a llantas/inventario)
        entradas_data = [
            {'talleres': taller, 'llantas': llanta_objs[0], 'producto_clave': inv_objs[0].producto_clave, 'precio': inv_objs[0].precio, 'cantidad': 4},
            {'talleres': taller, 'llantas': llanta_objs[1], 'producto_clave': inv_objs[1].producto_clave, 'precio': inv_objs[1].precio, 'cantidad': 2},
            {'talleres': taller, 'llantas': llanta_objs[2], 'producto_clave': inv_objs[2].producto_clave, 'precio': inv_objs[2].precio, 'cantidad': 1},
        ]
        for ed in entradas_data:
            obj, created_flag = Entradas.objects.get_or_create(
                talleres=ed['talleres'], llantas=ed['llantas'], producto_clave=ed['producto_clave'],
                defaults={'precio': ed['precio'], 'cantidad': ed['cantidad']}
            )
            if created_flag:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Creación de datos ejemplo completada. Objetos nuevos creados: {created}'))
