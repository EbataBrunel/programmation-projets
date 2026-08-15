package eajc.group.apv.entity;

import eajc.group.apv.enums.BeneficiaryType;
import jakarta.persistence.*;

import java.time.LocalDate;
import java.util.UUID;

@Entity
@Table(name = "beneficiaries")
public class Beneficiary {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, updatable = false)
    private UUID publicId;

    @Column(nullable = false)
    private String name;

    @Column(nullable = true)
    private String phone;

    @Column(nullable = true)
    private String email;

    @Column(nullable = false)
    private String address;

    @Column(nullable = false)
    private String country;

    @Column(nullable = false)
    private String city;

    @Column(nullable = false)
    private String borough;

    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    private BeneficiaryType type;

    @Column(nullable = false)
    private LocalDate dateExistence;

    public Beneficiary(){}

    public Beneficiary(Long id, UUID publicId, String name, String phone, String email, String address, String country, String city, String borough, BeneficiaryType type, LocalDate dateExistence) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
        this.phone = phone;
        this.email = email;
        this.address = address;
        this.country = country;
        this.city = city;
        this.borough = borough;
        this.type = type;
        this.dateExistence = dateExistence;
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

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public BeneficiaryType getType() {
        return type;
    }

    public void setType(BeneficiaryType type) {
        this.type = type;
    }

    public String getBorough() {
        return borough;
    }

    public void setBorough(String borough) {
        this.borough = borough;
    }

    public LocalDate getDateExistence() {
        return dateExistence;
    }

    public void setDateExistence(LocalDate dateExistence) {
        this.dateExistence = dateExistence;
    }

    @PrePersist
    protected void onCreate() {
        if (publicId == null) {
            publicId = UUID.randomUUID();
        }
    }
}
