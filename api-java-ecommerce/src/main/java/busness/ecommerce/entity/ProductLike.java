package busness.ecommerce.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(
        name = "product_like",
        uniqueConstraints = @UniqueConstraint(columnNames = {"user_id", "variant_id"})
)
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ProductLike {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "variant_id")
    private ProductVariant variant;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
}
