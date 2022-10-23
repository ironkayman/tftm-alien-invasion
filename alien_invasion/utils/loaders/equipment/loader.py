from alien_invasion.constants import DIR_EQUIPMENT

def load_equipment_from_categories():
  WEAPONRY = DIR_EQUIPMENT / 'weaponry'
  WEAPONRY.glob('*.json')