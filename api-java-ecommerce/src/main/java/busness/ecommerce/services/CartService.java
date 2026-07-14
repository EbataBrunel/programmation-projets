package busness.ecommerce.services;

import busness.ecommerce.dto.AttributeValueRequestDto;
import busness.ecommerce.dto.AttributeValueResponseDto;
import busness.ecommerce.dto.CartRequestDto;
import busness.ecommerce.dto.CartResponseDto;

import java.util.List;

public interface CartService {
    // POST
    CartResponseDto addToCart(Long userId, CartRequestDto dto);
    // GET
    CartResponseDto getCartByUser(Long userId);
    // GET
    CartResponseDto getCartById(Long id);
    // UPDATE
    CartResponseDto updateCart(Long id, CartRequestDto dto);
    // DELETE
    void deleteCartItem(Long id);
    // DELETE
    void deleteCart(Long id);
}
