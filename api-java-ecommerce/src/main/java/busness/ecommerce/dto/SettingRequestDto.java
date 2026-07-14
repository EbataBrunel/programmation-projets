package busness.ecommerce.dto;

import jakarta.persistence.Column;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SettingRequestDto {
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
