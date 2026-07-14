package busness.ecommerce.services;

import busness.ecommerce.dto.CartRequestDto;
import busness.ecommerce.dto.CartResponseDto;
import busness.ecommerce.entity.*;
import busness.ecommerce.mapper.CartMapper;
import busness.ecommerce.repository.CartItemRepository;
import busness.ecommerce.repository.CartRepository;
import busness.ecommerce.repository.ProductVariantRepository;
import busness.ecommerce.repository.UserRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional
public class CartServiceImpl implements CartService{

    private final CartRepository cartRepository;
    private final CartItemRepository cartItemRepository;
    private final ProductVariantRepository productRepository;
    private final UserRepository userRepository;
    private final CartMapper cartMapper;

    @Override
    public CartResponseDto addToCart(Long userId, CartRequestDto dto) {

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Cart cart = cartRepository.findByUser(user)
                .orElseGet(() -> {
                    Cart newCart = Cart.builder()
                            .user(user)
                            .items(new ArrayList<>())
                            .total(0.0)
                            .qtyTotal(0)
                            .build();
                    return cartRepository.save(newCart);
                });

        ProductVariant product = productRepository.findById(dto.getProductVariantId())
                .orElseThrow(() -> new RuntimeException("Product not found"));

        Optional<CartItem> existingItem =
                cart.getItems()
                        .stream()
                        .filter(i -> i.getProductVariant().getId().equals(product.getId()))
                        .findFirst();

        if (existingItem.isPresent()) {
            CartItem item = existingItem.get();
            item.setQuantity(item.getQuantity() + dto.getQuantity());
        } else {
            CartItem item = CartItem.builder()
                    .cart(cart)
                    .productVariant(product)
                    .quantity(dto.getQuantity())
                    .price(product.getPrice())
                    .build();

            cart.getItems().add(item);
        }

        double total = cart.getItems()
                .stream()
                .mapToDouble(i -> i.getPrice() * i.getQuantity())
                .sum();

        cart.setTotal(total);

        int qtyTotal = cart.getItems()
                .stream()
                .mapToInt(CartItem::getQuantity)
                .sum();

        cart.setQtyTotal(qtyTotal);

        return cartMapper.toDto(cartRepository.save(cart));
    }

    @Override
    public CartResponseDto getCartByUser(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Cart cart = cartRepository.findByUser(user)
                .orElseGet(() -> {
                    Cart newCart = Cart.builder()
                            .user(user)
                            .items(new ArrayList<>())
                            .total(0.0)
                            .qtyTotal(0)
                            .build();
                    return cartRepository.save(newCart);
                });


        return cartMapper.toDto(cart);
    }

    @Override
    public CartResponseDto getCartById(Long id) {
        Cart cart = cartRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Cart not found"));
        return cartMapper.toDto(cart);
    }

    @Override
    public CartResponseDto updateCart(Long id, CartRequestDto dto) {

        CartItem cartItem = cartItemRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("CartItem not found"));

        // modifier la quantité
        cartItem.setQuantity(dto.getQuantity());

        cartItemRepository.save(cartItem);

        Cart cart = cartItem.getCart();

        // recalcul total
        double total = cart.getItems()
                .stream()
                .mapToDouble(i -> i.getPrice() * i.getQuantity())
                .sum();

        cart.setTotal(total);

        // recalcul quantité totale
        int qtyTotal = cart.getItems()
                .stream()
                .mapToInt(CartItem::getQuantity)
                .sum();

        cart.setQtyTotal(qtyTotal);

        return cartMapper.toDto(cartRepository.save(cart));
    }

    @Override
    public void deleteCartItem(Long id) {
        CartItem cartItem = cartItemRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("CartItem not found"));
        cartItemRepository.delete(cartItem);
    }

    @Override
    public void deleteCart(Long id) {
        Cart cart = cartRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Cart not found"));
        cartRepository.delete(cart);
    }


}
