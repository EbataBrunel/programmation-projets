package eajc.group.apv.dto;

public class SettingRequestDto {
    private String nameApp;
    private String nameDev;
    private String version;
    private String theme;
    private String bodyTheme;
    private String textColor;
    private String currency;
    private String address;
    private String email;
    private String phone;
    private String logo;
    private Integer width;
    private Integer height;

    public SettingRequestDto(){}

    public SettingRequestDto(String nameApp, String nameDev, String version, String theme, String bodyTheme, String textColor, String currency, String address, String email, String phone, String logo, Integer width, Integer height) {
        this.nameApp = nameApp;
        this.nameDev = nameDev;
        this.version = version;
        this.theme = theme;
        this.bodyTheme = bodyTheme;
        this.textColor = textColor;
        this.currency = currency;
        this.address = address;
        this.email = email;
        this.phone = phone;
        this.logo = logo;
        this.width = width;
        this.height = height;
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
}
