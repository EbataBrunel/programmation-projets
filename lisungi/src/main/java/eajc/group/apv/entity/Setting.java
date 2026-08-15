package eajc.group.apv.entity;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.UUID;

@Entity
@Table(name = "settings")
public class Setting{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, updatable = false)
    private UUID publicId;

    @Column(nullable = false)
    private String nameApp;

    @Column(nullable = false)
    private String nameDev;

    @Column(nullable = false)
    private String version;

    @Column(nullable = false)
    private String theme;

    @Column(nullable = false)
    private String bodyTheme;

    @Column(nullable = false)
    private String textColor;

    @Column(nullable = false)
    private String currency;

    @Column(nullable = false)
    private String address;

    @Column(nullable = false)
    private String email;

    @Column(nullable = false)
    private String phone;

    @Column(nullable = false)
    private String logo;

    @Column(nullable = false)
    private Integer width;

    @Column(nullable = false)
    private Integer height;

    public Setting(){}

    public Setting(Long id, UUID publicId, String nameApp, String nameDev, String version, String bodyTheme, String theme, String textColor, String currency, String address, String email, String phone, String logo, Integer width, Integer height) {
        this.id = id;
        this.publicId = publicId;
        this.nameApp = nameApp;
        this.nameDev = nameDev;
        this.version = version;
        this.bodyTheme = bodyTheme;
        this.theme = theme;
        this.textColor = textColor;
        this.currency = currency;
        this.address = address;
        this.email = email;
        this.phone = phone;
        this.logo = logo;
        this.width = width;
        this.height = height;
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

    public String getNameApp() {
        return nameApp;
    }

    public void setNameApp(String nameApp) {
        this.nameApp = nameApp;
    }

    public String getNameDev() {
        return nameDev;
    }

    public void setNameDev(String nameDev) {
        this.nameDev = nameDev;
    }

    public String getVersion() {
        return version;
    }

    public void setVersion(String version) {
        this.version = version;
    }

    public String getTheme() {
        return theme;
    }

    public void setTheme(String theme) {
        this.theme = theme;
    }

    public String getBodyTheme() {
        return bodyTheme;
    }

    public void setBodyTheme(String bodyTheme) {
        this.bodyTheme = bodyTheme;
    }

    public String getTextColor() {
        return textColor;
    }

    public void setTextColor(String textColor) {
        this.textColor = textColor;
    }

    public String getCurrency() {
        return currency;
    }

    public void setCurrency(String currency) {
        this.currency = currency;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getLogo() {
        return logo;
    }

    public void setLogo(String logo) {
        this.logo = logo;
    }

    public Integer getWidth() {
        return width;
    }

    public void setWidth(Integer width) {
        this.width = width;
    }

    public Integer getHeight() {
        return height;
    }

    public void setHeight(Integer height) {
        this.height = height;
    }

    @PrePersist
    protected void onCreate() {
        if (publicId == null) {
            publicId = UUID.randomUUID();
        }
    }

}
