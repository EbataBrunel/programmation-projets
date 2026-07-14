package busness.ecommerce.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class BrandVariantCountResponseDto {
    private Long brandId;
    private String brandName;
    private Long variantCount;
}
