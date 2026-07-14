package busness.ecommerce.controller;

import busness.ecommerce.dto.LikedVariantResponseDto;
import busness.ecommerce.dto.ProductLikeRequestDto;
import busness.ecommerce.dto.ProductLikeResponseDto;
import busness.ecommerce.dto.VariantLikeUserDto;
import busness.ecommerce.entity.User;
import busness.ecommerce.repository.UserRepository;
import busness.ecommerce.services.LikeService;
import busness.ecommerce.services.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping("/api/v1/likes")
@RequiredArgsConstructor
public class ProductLikeRestController {
    private final LikeService likeService;
    private final UserService userService;

    // Ajouter un like
    /*@PostMapping
    public ResponseEntity<ProductLikeResponseDto> create(
            @RequestBody ProductLikeRequestDto dto
    ){
        return ResponseEntity.ok(likeService.addLike(dto));
    }*/

    @GetMapping("/check/{variantId}")
    public ResponseEntity<Boolean> hasLiked(
            @PathVariable Long variantId) {

        User user = userService.getCurrentUser();

        boolean liked = likeService.existsByUserIdAndVariantId(user.getId(), variantId);

        return ResponseEntity.ok(liked);
    }

    @PostMapping("/toggle/{variantId}")
    public ResponseEntity<Boolean> toggleLike(
            @PathVariable Long variantId) {

        User user = userService.getCurrentUser();

        boolean liked = likeService.toggleLike(user.getId(), variantId);

        return ResponseEntity.ok(liked);
    }

    @GetMapping("/variant/{variantId}/users")
    public ResponseEntity<List<VariantLikeUserDto>> getUsersWhoLiked(
            @PathVariable Long variantId) {

        return ResponseEntity.ok(
                likeService.getUsersWhoLiked(variantId)
        );
    }

    @GetMapping("/my-likes")
    public ResponseEntity<List<LikedVariantResponseDto>> getMyLikes() {

        User user = userService.getCurrentUser();

        return ResponseEntity.ok(
                likeService.getLikedVariants(user.getId())
        );
    }

    // Supprimer un like
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        likeService.deleteLike(id);
        return ResponseEntity.noContent().build();
    }
}
