package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class AttributeValueResponseDto {
    private Long id;
    private String value;
    private Long attributeId;
    private String attributeName;
}
