package busness.ecommerce.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class VariantProductCategoryCountResponseDto {
   Long productCategoryId;
   String productCategoryName;
   Long countVariant;
}
