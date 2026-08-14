package eajc.group.apv.entity;

import jakarta.persistence.*;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
public class EventType {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, updatable = false)
    private UUID publicId;

    @Column(unique = true, nullable = false, length = 200)
    private String name;

    @OneToMany(mappedBy = "eventType", cascade = CascadeType.ALL)
    private List<Event> events = new ArrayList<>();

    public EventType(){}

    public EventType(Long id, UUID publicId, String name) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
    }

    public EventType(Long id, UUID publicId, String name, List<Event> events) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
        this.events = events;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public UUID getPublicId() {
        return publicId;
    }

    public void setPublicId(UUID publicId) {
        this.publicId = publicId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @PrePersist
    protected void onCreate() {
        if (publicId == null) {
            publicId = UUID.randomUUID();
        }
    }

    public List<Event> getEvents() {
        return events;
    }

    public void setEvents(List<Event> events) {
        this.events = events;
    }
}
