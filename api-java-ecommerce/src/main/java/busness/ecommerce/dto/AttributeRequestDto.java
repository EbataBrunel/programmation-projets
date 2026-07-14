package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class AttributeRequestDto {
    private String name;
}
