package busness.ecommerce.entity;

import busness.ecommerce.enums.ProductSource;
import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import lombok.*;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // commande
    @ManyToOne
    @JoinColumn(name = "order_id")
    @JsonBackReference
    private Order order;

    // produit, lien technique (optionnel mais utile)
    @ManyToOne
    @JoinColumn(name = "product_variant_id")
    private ProductVariant productVariant;

    // SNAPSHOT IMMUTABLE
    private String productName;
    private String sku;
    private Double price; // prix au moment de l'achat (Prix unitaire)

    private Integer quantity;

    // Snapshot vendeur
    @ManyToOne
    private User seller;

    // SNAPSHOT SOURCE
    @Enumerated(EnumType.STRING)
    private ProductSource productSource;
}

