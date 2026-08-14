package eajc.group.apv.entity;

import jakarta.persistence.*;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "donations")
public class Donation {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, updatable = false)
    private UUID publicId;

    @Column(unique = true, nullable = false, length = 300)
    private String title;

    @Column(nullable = false)
    private LocalDate dateDonation;

    @Column(nullable = false)
    private Boolean closure_status;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String description;

    @ManyToOne
    @JoinColumn(name = "beneficiary_id")
    private Beneficiary beneficiary;

    @Column(unique = true, nullable = true)
    private String photo;

    @Column(nullable = false)
    private Boolean publicStatus;

    @OneToMany(mappedBy = "donation", cascade = CascadeType.ALL)
    private List<DonationParticipant> participants = new ArrayList<>();

    public Donation(){}

    public Donation(Long id, UUID publicId, String title, LocalDate dateDonation, Boolean closure_status, String description, Beneficiary beneficiary, String photo, Boolean publicStatus, List<DonationParticipant> participants) {
        this.id = id;
        this.publicId = publicId;
        this.title = title;
        this.dateDonation = dateDonation;
        this.closure_status = closure_status;
        this.description = description;
        this.beneficiary = beneficiary;
        this.photo = photo;
        this.publicStatus = publicStatus;
        this.participants = participants;
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

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public LocalDate getDateDonation() {
        return dateDonation;
    }

    public void setDateDonation(LocalDate dateDonation) {
        this.dateDonation = dateDonation;
    }

    public Boolean getClosure_status() {
        return closure_status;
    }

    public void setClosure_status(Boolean closure_status) {
        this.closure_status = closure_status;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Beneficiary getBeneficiary() {
        return beneficiary;
    }

    public void setBeneficiary(Beneficiary beneficiary) {
        this.beneficiary = beneficiary;
    }

    public String getPhoto() {
        return photo;
    }

    public void setPhoto(String photo) {
        this.photo = photo;
    }

    public Boolean getPublicStatus() {
        return publicStatus;
    }

    public void setPublicStatus(Boolean publicStatus) {
        this.publicStatus = publicStatus;
    }

    public List<DonationParticipant> getParticipants() {
        return participants;
    }

    public void setParticipants(List<DonationParticipant> participants) {
        this.participants = participants;
    }

    @PrePersist
    protected void onCreate() {
        if (publicId == null) {
            publicId = UUID.randomUUID();
        }

        if (closure_status == null){
            closure_status = false;
        }

        if (publicStatus == null){
            publicStatus = true;
        }
    }
}
