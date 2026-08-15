package eajc.group.apv.enums;

public enum Reason {
    JE_SUIS_INTERESSE("Je suis intéressé"),
    JE_NE_SUIS_PLUS_INTERESSE("Je ne suis plus intéressé"),
    JE_NE_SUIS_PLUS_DISPONIBLE("Je ne suis plus disponible"),
    JE_VAIS_PRENDRE_UNE_PAUSE("Je vais prendre une pause"),
    ORGANISATION_N_EST_PAS_BONNE("L'organisation n'est pas bonne"),
    AUTRES("Autres");

    private final String label;

    Reason(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}
