package busness.ecommerce.entity;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Data
public class ProductImage {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String url;   // chemin image

    private boolean mainImage;

    @ManyToOne
    private Product product;
}

