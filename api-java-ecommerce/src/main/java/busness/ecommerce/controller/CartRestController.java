package busness.ecommerce.controller;

import busness.ecommerce.dto.CartRequestDto;
import busness.ecommerce.dto.CartResponseDto;
import busness.ecommerce.dto.CategoryRequestDto;
import busness.ecommerce.dto.CategoryResponseDto;
import busness.ecommerce.entity.Cart;
import busness.ecommerce.services.CartService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequiredArgsConstructor
@RequestMapping(value = "/api/v1/cart")
public class CartRestController {
    private final CartService cartService;

    @PostMapping("/add/{userId}")
    public ResponseEntity<CartResponseDto> addToCart(
            @PathVariable Long userId,
            @RequestBody CartRequestDto dto
    ) {
        //System.out.println("Hello, World!");
        return ResponseEntity.ok(cartService.addToCart(userId, dto));
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<CartResponseDto> getUserCart(
            @PathVariable Long userId
    ) {
        return ResponseEntity.ok(cartService.getCartByUser(userId));
    }

    // Récupérer un panier par id
    @GetMapping("/{id}")
    public ResponseEntity<CartResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(cartService.getCartById(id));
    }

    // Modifier un panier
    @PutMapping("/{id}")
    public ResponseEntity<CartResponseDto> update(
            @PathVariable Long id,
            @RequestBody CartRequestDto dto
    ) {
        return ResponseEntity.ok(cartService.updateCart(id, dto));
    }

    // Supprimer un panier
    @DeleteMapping("/cartItem/{id}")
    public ResponseEntity<Void> deleteCartItem(
            @PathVariable Long id
    ) {
        cartService.deleteCartItem(id);
        return ResponseEntity.noContent().build();
    }

    // Supprimer un panier
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        cartService.deleteCart(id);
        return ResponseEntity.noContent().build();
    }
}
