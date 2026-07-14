package busness.ecommerce.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "attributes")
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Attribute {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false)
    private String name; // taille, couleur, matière

    @OneToMany(mappedBy = "attribute", cascade = CascadeType.ALL)
    private List<AttributeValue> attributeValues = new ArrayList<>();
}

