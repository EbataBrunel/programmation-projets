package eajc.group.apv.dto;

import java.math.BigDecimal;
import java.util.UUID;

public class ContributionsByEventCountDto {
    private Long id;
    private UUID publicId;
    private String name;
    private boolean closure_status;
    private BigDecimal mount;
    private BigDecimal amountTotal;
    private Long totalContribution;

    public ContributionsByEventCountDto(){}

    public ContributionsByEventCountDto(Long id, UUID publicId, String name, boolean closure_status, BigDecimal mount, BigDecimal amountTotal, Long totalContribution) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
        this.closure_status = closure_status;
        this.mount = mount;
        this.amountTotal = amountTotal;
        this.totalContribution = totalContribution;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public UUID getPublicId() {
        return publicId;
    }

    public void setPublicId(UUID publicId) {
        this.publicId = publicId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public boolean isClosure_status() {
        return closure_status;
    }

    public void setClosure_status(boolean closure_status) {
        this.closure_status = closure_status;
    }

    public BigDecimal getMount() {
        return mount;
    }

    public void setMount(BigDecimal mount) {
        this.mount = mount;
    }

    public BigDecimal getAmountTotal() {
        return amountTotal;
    }

    public void setAmountTotal(BigDecimal amountTotal) {
        this.amountTotal = amountTotal;
    }

    public Long getTotalContribution() {
        return totalContribution;
    }

    public void setTotalContribution(Long totalContribution) {
        this.totalContribution = totalContribution;
    }
}
