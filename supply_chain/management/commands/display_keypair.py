from django.core.management.base import BaseCommand
from supply_chain.solana_integration import display_keypair_info

class Command(BaseCommand):
    help = 'Display Solana keypair information'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Displaying Solana keypair information:'))
        try:
            display_keypair_info()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error displaying keypair information: {str(e)}'))
