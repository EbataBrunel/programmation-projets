package eajc.group.apv.dto;

import java.util.UUID;

public class ContributedCountDTO {
    private Long contributedId;
    private UUID contributedPublicId;
    private String firstName;
    private String lastName;
    private Long contributionCount;

    public ContributedCountDTO(Long contributedId, UUID contributedPublicId, String firstName, String lastName, Long contributionCount) {
        this.contributedId = contributedId;
        this.contributedPublicId = contributedPublicId;
        this.firstName = firstName;
        this.lastName = lastName;
        this.contributionCount = contributionCount;
    }

    public Long getContributedId() {
        return contributedId;
    }

    public void setContributedId(Long contributedId) {
        this.contributedId = contributedId;
    }

    public UUID getContributedPublicId() {
        return contributedPublicId;
    }

    public void setContributedPublicId(UUID contributedPublicId) {
        this.contributedPublicId = contributedPublicId;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public Long getContributionCount() {
        return contributionCount;
    }

    public void setContributionCount(Long contributionCount) {
        this.contributionCount = contributionCount;
    }
}
