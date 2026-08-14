package eajc.group.apv.entity;

import eajc.group.apv.enums.DonationItemType;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;


@Entity
@Table(name = "donation_participants")
public class DonationParticipant {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, updatable = false)
    private UUID publicId;

    @Column(unique = true, nullable = false, length = 200)
    private String name;

    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    private DonationItemType itemType;

    @Column(nullable = true)
    private String description;

    @Column(nullable = true)
    private BigDecimal amount; // uniquement si itemType == MONEY

    @Column(nullable = false)
    private LocalDateTime participationDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "donation_id", nullable = false)
    private Donation donation;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    public DonationParticipant(){}

    public DonationParticipant(Long id, UUID publicId, String name, DonationItemType itemType, String description, BigDecimal amount, LocalDateTime participationDate, Donation donation, User user) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
        this.itemType = itemType;
        this.description = description;
        this.amount = amount;
        this.participationDate = participationDate;
        this.donation = donation;
        this.user = user;
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

    public DonationItemType getItemType() {
        return itemType;
    }

    public void setItemType(DonationItemType itemType) {
        this.itemType = itemType;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public BigDecimal getAmount() {
        return amount;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public LocalDateTime getParticipationDate() {
        return participationDate;
    }

    public void setParticipationDate(LocalDateTime participationDate) {
        this.participationDate = participationDate;
    }

    public Donation getDonation() {
        return donation;
    }

    public void setDonation(Donation donation) {
        this.donation = donation;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    @PrePersist
    protected void onCreate() {
        if (publicId == null) {
            publicId = UUID.randomUUID();
        }

        if (participationDate == null){
            participationDate = LocalDateTime.now();
        }

    }
}
