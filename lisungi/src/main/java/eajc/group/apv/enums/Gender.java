package eajc.group.apv.enums;

import com.fasterxml.jackson.annotation.JsonCreator;

public enum Gender {
    MASCULIN,
    FEMININ;

    @JsonCreator
    public static Gender fromValue(String value) {

        return Gender.valueOf(value.toUpperCase());
    }
}
