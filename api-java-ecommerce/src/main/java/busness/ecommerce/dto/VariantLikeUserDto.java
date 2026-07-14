package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class VariantLikeUserDto {
    Long userId;
    private String firstName;
    private String lastName;
}
