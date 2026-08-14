package eajc.group.apv.enums;

import com.fasterxml.jackson.annotation.JsonCreator;

public enum BeneficiaryType {
    PARTICULIER,
    ORPHELINAT,
    ASSOCIATION,
    EGLISE,
    ECOLE,
    ONG,
    AUTRE;

    @JsonCreator
    public static BeneficiaryType fromValue(String value) {
        return BeneficiaryType.valueOf(value.toUpperCase());
    }
}
