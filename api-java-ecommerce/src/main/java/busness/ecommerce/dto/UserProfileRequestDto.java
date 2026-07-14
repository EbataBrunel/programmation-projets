package busness.ecommerce.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class UserProfileRequestDto {

    private String firstName;
    private String lastName;
    private String phone;
    private String address;
    private Long userId;
    private String country;
    private String city;
    private String borough;
    private String photo;
}
