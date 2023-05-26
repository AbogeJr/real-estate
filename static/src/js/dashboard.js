/** @odoo-module **/
const { Component, useSubEnv, onWillStart, whenReady, xml, mount, useState } =
  owl;
import { getDefaultConfig } from "@web/views/view";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";
import { Card } from "./card/card";
import { PieChart } from "./chart/chart";

class App extends Component {
  setup() {
    useSubEnv({
      config: {
        ...getDefaultConfig(),
        ...this.env.config,
      },
    });

    this.display = {
      controlPanel: { "top-right": false, "bottom-right": false },
    };
    this.action = useService("action");
    this.estateService = useService("estateService");
    this.keyToString = {
      avg_price: "Average selling price of properties",
      count: "Number of properties",
    };
    // this.rpc = useService("rpc");
    onWillStart(async () => {
      this.statistics = await this.estateService.loadStatistics();
      console.log("Statistiscs", this.statistics);
    });
  }
  increment() {
    this.state.counter++;
  }

  state = useState({ counter: 0 });

  openProperty(title, domain) {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: title,
      res_model: "estate.property",
      domain: new Domain(domain).toList(),
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }
  openNewProperties() {
    const domain = "[('state','=', 'new')]";
    this.openProperty("Estate Properties", domain);
  }
  openSoldProperties() {
    const domain = "[('state','=', 'sold')]";
    this.openProperty("Estate Properties", domain);
  }
}

App.template = "real_estate.Dashboard";
App.components = { Layout, Card, PieChart };

registry.category("actions").add("real-estate.dashboard", App);
