import pandas as pd
from composition.models import Composer
from app_auth.models import Student
from matiere.models import Matiere
from salle.models import Salle
# Récommandation 
def get_data(anneeacademique_id, classe_id):
    
    notes = Composer.objects.filter(anneeacademique_id=anneeacademique_id).values(
        'student__id', 'salle__id', 'matiere__id', 'note'
    )
    return pd.DataFrame(notes)

def detect_problemes(df):
    alertes = []
    for student_id, groupe in df.groupby('student__id'):
        salle_id = groupe['salle__id'].iloc[0]
        student = Student.objects.get(id=student_id)
        salle = Salle.objects.get(id=salle_id)
        moyennes = groupe.groupby('matiere__id')['note'].mean()
        for matiere_id, moyenne in moyennes.items():
            matiere = Matiere.objects.get(id=matiere_id)
            if moyenne < 20:
                alertes.append({
                    'student': student,
                    'salle': salle,
                    'matiere': matiere,
                    'moyenne': round(moyenne, 2),
                    'recommandation': f"Renforcement recommandé en {matiere}"
                })
    return alertes