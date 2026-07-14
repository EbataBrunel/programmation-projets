package busness.ecommerce.repository;

import busness.ecommerce.entity.ProductImage;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface ProductImageRepository extends JpaRepository<ProductImage, Long> {
    List<ProductImage> findByProductId(Long productId);

    Optional<ProductImage> findByProductIdAndMainImageTrue(Long productId);
}
