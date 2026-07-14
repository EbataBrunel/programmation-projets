package busness.ecommerce.mapper;

import busness.ecommerce.dto.CartItemResponseDto;
import busness.ecommerce.dto.CartResponseDto;
import busness.ecommerce.entity.Cart;
import busness.ecommerce.entity.CartItem;
import busness.ecommerce.entity.Product;
import busness.ecommerce.entity.ProductVariant;
import org.springframework.stereotype.Component;

@Component
public class CartMapper {
    public CartResponseDto toDto(Cart cart) {

        return CartResponseDto.builder()
                .id(cart.getId())
                .userId(cart.getUser().getId())
                .items(
                        cart.getItems().stream()
                                .map(this::mapItem)
                                .toList()
                )
                .total(cart.getTotal())
                .qtyTotal(cart.getQtyTotal())
                .build();
    }

    private CartItemResponseDto mapItem(CartItem item) {
        ProductVariant variant = item.getProductVariant();
        Product product = variant.getProduct();

        String imageUrl = product.getImages()
                .stream()
                .filter(img -> Boolean.TRUE.equals(img.isMainImage()))
                .map(img -> img.getUrl())
                .findFirst()
                .orElse(null);

        return CartItemResponseDto.builder()
                .id(item.getId())
                .productVariantId(variant.getId())
                .productName(product.getName())
                .productImageUrl(imageUrl)
                .price(item.getPrice())
                .quantity(item.getQuantity())
                .subTotal(item.getPrice() * item.getQuantity())
                .build();
    }
}
