package busness.ecommerce.dto;

import lombok.Builder;
import lombok.Data;
import java.util.List;

@Data
@Builder
public class CartResponseDto {

    private Long id;
    // juste l'id du user
    private Long userId;

    private List<CartItemResponseDto> items;

    private Double total;

    private Integer qtyTotal;

}

