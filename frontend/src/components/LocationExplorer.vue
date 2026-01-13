<template>
  <div>
    <p v-if="!lieux || lieux.length === 0">Aucune donnée disponible.</p>
    <v-treeview
      v-else
      :items="lieux"
      item-key="id"
      :open-on-click="false"
      item-text="nomLieu"
      rounded
      hoverable
      activatable
      dense
      @update:active="on_select"
    >
    <template v-slot:prepend="{ item, open }">
      <v-icon
        v-if="item.children && item.children.length > 0 && item.nomLieu !== 'Tous'"
        @click.stop="toggle_node(item)"
        :class="{ 'rotate-icon': open }"
      >
        {{ open ? 'mdi-triangle-down' : 'mdi-triangle-right' }}
      </v-icon>
      <span v-else class="tree-icon-placeholder"></span>
      {{ item.nomLieu }}
    </template>
      <template v-slot:label="{ item }">
        <span class="text-caption ml-2">{{ item.typeLieu }}</span>
      </template>
    </v-treeview>
  </div>
</template>

<script>
import { VTreeView } from 'vuetify/components'

export default {
  name: 'LocationExplorer',
  components: {
    VTreeView
  },
  props: {
    lieux: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      open_nodes: new Set(),
    };
  },
  methods: {
    on_select(items) {
      if (items.length > 0) {
        const selected_item = this.find_item(this.lieux, items[0]);
        if (selected_item) {
          this.$emit('select-lieu', selected_item);
        }
      }
    },
    find_item(items, id) {
      for (const item of items) {
        if (item.id === id) {
          return item;
        }
        if (item.children) {
          const found = this.find_item(item.children, id);
          if (found) {
            return found;
          }
        }
      }
      return null;
    },
    toggle_node(item) {
      if (this.open_nodes.has(item.id)) {
        this.open_nodes.delete(item.id);
      } else {
        this.open_nodes.add(item.id);
      }
      this.$forceUpdate();
    },
  }
}
</script>

<style scoped>
.text-caption {
  color: #666;
  font-size: 0.75rem;
}

.tree-icon-placeholder {
  display: inline-block;
  width: 24px;
  height: 24px;
  margin-right: 4px;
}

.rotate-icon {
  transform: rotate(180deg);
}

.v-icon {
  transition: transform 0.3s ease;
}
</style>