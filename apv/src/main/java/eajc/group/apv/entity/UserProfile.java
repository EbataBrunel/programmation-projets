package eajc.group.apv.entity;

import eajc.group.apv.enums.Gender;
import eajc.group.apv.enums.Reason;
import jakarta.persistence.*;

import java.time.LocalDate;
import java.util.UUID;

@Entity
public class UserProfile {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, updatable = false)
    private UUID publicId;

    private String firstName;
    private String lastName;
    @Enumerated(EnumType.STRING)
    private Gender gender;
    private String phone;
    private String address;
    private String country;
    private String city;
    private String borough;
    private String profession;
    private String photo;
    private LocalDate registrationDate;
    @Enumerated(EnumType.STRING)
    private Reason reasonRemoval;

    @OneToOne
    @JoinColumn(name = "user_id")
    private User user;

    public UserProfile(){}

    public UserProfile(Long id, UUID publicId, String firstName, Gender gender, String lastName, String phone, String address, String country, String city, String borough, String profession, String photo, LocalDate registrationDate, Reason reasonRemoval, User user) {
        this.id = id;
        this.publicId = publicId;
        this.firstName = firstName;
        this.gender = gender;
        this.lastName = lastName;
        this.phone = phone;
        this.address = address;
        this.country = country;
        this.city = city;
        this.borough = borough;
        this.profession = profession;
        this.photo = photo;
        this.registrationDate = registrationDate;
        this.reasonRemoval = reasonRemoval;
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

    public Gender getGender() {
        return gender;
    }

    public void setGender(Gender gender) {
        this.gender = gender;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
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

    public String getBorough() {
        return borough;
    }

    public void setBorough(String borough) {
        this.borough = borough;
    }

    public String getProfession() {
        return profession;
    }

    public void setProfession(String profession) {
        this.profession = profession;
    }

    public String getPhoto() {
        return photo;
    }

    public void setPhoto(String photo) {
        this.photo = photo;
    }

    public LocalDate getRegistrationDate() {
        return registrationDate;
    }

    public void setRegistrationDate(LocalDate registrationDate) {
        this.registrationDate = registrationDate;
    }

    public Reason getReasonRemoval() {
        return reasonRemoval;
    }

    public void setReasonRemoval(Reason reasonRemoval) {
        this.reasonRemoval = reasonRemoval;
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

        if (registrationDate == null){
            registrationDate = LocalDate.now();
        }

        if (reasonRemoval == null) {
            reasonRemoval = Reason.JE_SUIS_INTERESSE;        }
    }
}
