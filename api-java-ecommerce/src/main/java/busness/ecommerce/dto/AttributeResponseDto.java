package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Data
@Builder
public class AttributeResponseDto {
    Long id;
    String name;
    List<AttributeValueResponseDto> attributeValues = new ArrayList<>();
}
