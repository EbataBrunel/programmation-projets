package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class SettingResponseDto {
    private Long id;
    private String nameApp;
    private String nameDev;
    private String version;
    private String theme;
    private String textColor;
    private String currency;
    private String address;
    private String email;
    private String phone;
    private String logo;
    private Integer width;
    private Integer height;
}
