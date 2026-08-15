package eajc.group.apv.dto;

import eajc.group.apv.enums.Reason;

public class UserProfileReasonRemovalDto {

    private Reason reasonRemoval;

    public UserProfileReasonRemovalDto(){}

    public UserProfileReasonRemovalDto(Reason reasonRemoval) {
        this.reasonRemoval = reasonRemoval;
    }

    public Reason getReasonRemoval() {
        return reasonRemoval;
    }

    public void setReasonRemoval(Reason reasonRemoval) {
        this.reasonRemoval = reasonRemoval;
    }
}
